import {copyFileSync, mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const docsDir = resolve(scriptDir, '../..');
const staticDir = resolve(scriptDir, '../static');

mkdirSync(resolve(staticDir, 'Media'), {recursive: true});
copyFileSync(resolve(docsDir, 'Veil.html'), resolve(staticDir, 'Veil.html'));
copyFileSync(resolve(docsDir, 'Media/Veil.svg'), resolve(staticDir, 'Media/Veil.svg'));