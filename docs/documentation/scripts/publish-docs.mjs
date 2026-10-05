import {cpSync, mkdirSync, rmSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const buildDir = resolve(scriptDir, '../build');
const publishDir = resolve(scriptDir, '../../manual');

rmSync(publishDir, {recursive: true, force: true});
mkdirSync(publishDir, {recursive: true});
cpSync(buildDir, publishDir, {recursive: true});