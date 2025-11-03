import { killPort } from '@nx/node/utils';
// global-teardown.ts

module.exports = async function () {
  // Put clean up logic here (e.g. stopping services, docker-compose, etc.).
  // Hint: `globalThis` is shared between setup and teardown.
  
  // Clean up the backend process we started
  if (globalThis.__BACKEND_PROCESS__) {
    globalThis.__BACKEND_PROCESS__.kill('SIGTERM');
  }
  
  const port = process.env.PORT ? Number(process.env.PORT) : 3000;
  await killPort(port);
  console.log(globalThis.__TEARDOWN_MESSAGE__);
};
