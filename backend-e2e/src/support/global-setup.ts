import { waitForPortOpen } from '@nx/node/utils';
import { spawn } from 'child_process';
import { join } from 'path';

// global-setup.ts
// Use globalThis for teardown message, no need for var/let/const

module.exports = async function () {
  // Start services that that the app needs to run (e.g. database, docker-compose, etc.).
  console.log('\nSetting up...\n');

  const host = process.env.HOST ?? 'localhost';
  const port = process.env.PORT ? Number(process.env.PORT) : 3000;

  // Start the backend server directly using our fixed approach
  const backendPath = join(process.cwd(), 'backend', 'dist', 'main.js');
  const backendProcess = spawn('node', [backendPath], {
    env: { ...process.env, NODE_ENV: 'development' },
    stdio: 'inherit',
    detached: false
  });

  // Store the process in globalThis so we can clean it up later
  globalThis.__BACKEND_PROCESS__ = backendProcess;

  await waitForPortOpen(port, { host });

  // Hint: Use `globalThis` to pass variables to global teardown.
  globalThis.__TEARDOWN_MESSAGE__ = '\nTearing down...\n';
};
