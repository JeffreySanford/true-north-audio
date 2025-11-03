import { ExecutorContext } from '@nx/devkit';
import { execSync } from 'child_process';

export interface PythonExecutorOptions {
  command: string;
  args?: string[];
  cwd?: string;
  pythonPath?: string;
  env?: Record<string, string>;
}

export default async function pythonExecutor(
  options: PythonExecutorOptions,
  context: ExecutorContext
): Promise<{ success: boolean }> {
  try {
    const cwd = options.cwd || context.cwd;
    const pythonPath = options.pythonPath || 'python';

    // Set up environment variables
    const env = {
      ...process.env,
      PYTHONPATH: [
        cwd,
        process.env.PYTHONPATH
      ].filter(Boolean).join(':'),
      ...options.env
    };

    // Build the command
    const args = options.args || [];
    const fullCommand = `${pythonPath} ${options.command} ${args.join(' ')}`;

    console.log(`Running: ${fullCommand} in ${cwd}`);

    // Execute the command
    execSync(fullCommand, {
      cwd,
      env,
      stdio: 'inherit'
    });

    return { success: true };
  } catch (error) {
    console.error(`Python executor failed:`, error);
    return { success: false };
  }
}