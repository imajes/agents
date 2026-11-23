#!/usr/bin/env python3
"""Validate the review skeleton, not an unimplemented product runtime."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys


def validate(root, source=None, marketplace=None):
    errors = []
    checks = []

    def check(condition, message):
        checks.append(message)
        if not condition:
            errors.append(message)

    manifest = json.loads((root / 'plugin.json').read_text())
    catalog = json.loads((root / 'catalog.json').read_text())
    check(manifest['name'] == 'veracity-actions', 'Stable plugin identity')
    check(manifest['version'] == catalog['version'] and 'skeleton' in manifest['version'], 'Version explicitly identifies skeleton')
    check(manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'Portable manifest schema declared')
    check(catalog['status'] == 'skeleton', 'Catalog identifies skeleton')
    extension = manifest['extensions']['com.openai']
    check(not {'apps', 'hooks', 'mcpServers', 'onboardingSkill'}.intersection(extension), 'No runtime or automatic onboarding declared')
    check(extension['interface']['capabilities'] == ['Interactive'], 'No unimplemented read/write/MCP capability advertised')
    check(not any((root / p).exists() for p in ('mcp.json', '.mcp.json', '.app.json', 'hooks', '.codex-plugin')), 'No server, app, hook, or divergent compatibility manifest shipped')

    entries = catalog['skills']
    names = {entry['name'] for entry in entries}
    check(len(names) == len(entries), 'Unique skill names')
    check({p.parent.name for p in (root / 'skills').glob('*/SKILL.md')} == names, 'Catalog matches packaged skills')
    known_caps = set(catalog['capabilities'])
    known_sections = set(catalog['source_dispositions'])
    for cap in catalog['capabilities'].values():
        check(cap['status'] == 'not-implemented', 'Capability explicitly unimplemented: ' + cap['title'])
    for entry in entries:
        name = entry['name']
        folder = root / 'skills' / name
        body = (folder / 'SKILL.md').read_text()
        metadata = (folder / 'agents/openai.yaml').read_text()
        header = re.match(r'^---\n(.*?)\n---\n', body, re.S)
        check(header is not None, name + ': frontmatter exists')
        check(bool(header and re.search(r'^name: '+re.escape(name)+r'$', header[1], re.M)), name + ': declared name matches folder')
        check('**Status: skeleton / not implemented.**' in body, name + ': visible stub status')
        check('Do not activate ongoing controls, execute the intended workflow' in body, name + ': preview-only execution boundary')
        check(bool(re.search(r'^policy:\n  allow_implicit_invocation: false\s*$', metadata, re.M)), name + ': explicit invocation policy')
        check('dependencies:' not in metadata, name + ': no nonexistent tool dependency')
        prompt_match = re.search(r'^  default_prompt: (.+)$', metadata, re.M)
        prompt = json.loads(prompt_match[1]) if prompt_match else ''
        check('$'+name in prompt, name + ': invocation example selects this skill')
        check(entry['status'] == 'stub', name + ': catalog status is stub')
        check(bool(entry['inputs'] and entry['outputs'] and entry['modes'] and entry['boundary']), name + ': actionable input/output/scope contract')
        check(bool(entry['negative_example'] and entry['design_question']), name + ': negative case and open design choice')
        check(set(entry['capabilities']) <= known_caps, name + ': all dependency contracts resolve')
        check(set(entry['source_sections']) <= known_sections, name + ': all source sections mapped')

    for section, disposition in catalog['source_dispositions'].items():
        check(set(disposition['skills']) <= names, section + ': source disposition references packaged skills')
    for command, name in catalog['command_map'].items():
        check(name in names, command + ': command has a skill')

    link_count = 0
    for path in root.rglob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            link_count += 1
            target = (path.parent / link.split('#', 1)[0]).resolve()
            check(target.is_relative_to(root) and target.exists(), str(path.relative_to(root)) + ': packaged link ' + link)
    check(not any(p.is_symlink() for p in root.rglob('*')), 'Package has no external symlink dependencies')

    if source:
        raw = source.read_bytes()
        text = raw.decode('utf-8')
        sections = set(re.findall(r'^### ((?:0\.\d+|[A-F]\d+)(?:\.\d+)*) —', text, re.M))
        if re.search(r'^## Module G —', text, re.M):
            sections.add('G')
        check(hashlib.sha256(raw).hexdigest() == catalog['source']['sha256'], 'Reference source matches recorded digest')
        check(sections == known_sections, 'Every actual labeled source section has a disposition, with no invented sections')
        command_block = text.split('### D6 —', 1)[1].split('When exploration ends:', 1)[0]
        actual = re.findall(r'^- `([^`]+)`', command_block, re.M)
        check(len(actual) == 15, 'Source command grammar still contains the inspected fifteen forms')
        normalized = []
        for command in actual:
            if command.startswith('EXPLORE '):
                name = 'EXPLORE 1 / EXPLORE N'
            elif command == 'RESUME':
                name = 'RESUME (prior focus)'
            elif command.startswith('PROMOTE '):
                name = 'PROMOTE ... TO PROJECT'
            else:
                name = re.sub(r':.*| <.*', '', command)
            normalized.append(name)
        check(set(normalized) == set(catalog['command_map']), 'All actual explicit command forms mapped')

    if marketplace:
        market = json.loads(marketplace.read_text())
        matches = [e for e in market['plugins'] if e['name'] == manifest['name']]
        check(len(matches) == 1, 'Exactly one marketplace entry')
        if len(matches) == 1:
            entry = matches[0]
            source_path = entry['source']['path']
            check(source_path.startswith('./'), 'Local marketplace path is explicitly relative')
            market_root = marketplace.parent.parent.parent
            check((market_root / source_path).resolve() == root, 'Marketplace resolves to the qualified package')
            check(entry['policy']['installation'] == 'AVAILABLE', 'Marketplace does not auto-install the skeleton')

    return {'passed': not errors, 'checks': len(checks), 'skills': len(entries),
            'source_sections': len(known_sections), 'command_families': len(catalog['command_map']),
            'capabilities': len(known_caps), 'local_links': link_count,
            'scope': 'Static skeleton validation only; no host activation or runtime behavior tested.', 'errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Optionally check the exact contract source and coverage')
    parser.add_argument('--marketplace', type=Path, help='Optionally check this promoted package’s catalog entry')
    args = parser.parse_args()
    try:
        result = validate(Path(__file__).resolve().parents[1], args.source, args.marketplace)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'passed': False, 'errors': [str(exc)]}
    print(json.dumps(result, indent=2))
    sys.exit(0 if result['passed'] else 1)
