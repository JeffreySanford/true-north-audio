// TypeScript type declaration
export type WorkspaceLoggerType = InstanceType<typeof WorkspaceLogger>;
import * as fs from 'fs';
import * as path from 'path';

export class WorkspaceLogger {
  private logPath: string;
  constructor(logDir = 'logs') {
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir);
    }
    const timestamp = new Date().toISOString().replace(/[:.]/g, '_');
    this.logPath = path.join(logDir, `workspace_${timestamp}.log`);
  }

  info(msg: string) {
    fs.appendFileSync(this.logPath, `${new Date().toISOString()} - INFO - ${msg}\n`);
  }

  error(msg: string) {
    fs.appendFileSync(this.logPath, `${new Date().toISOString()} - ERROR - ${msg}\n`);
  }

  getLogPath() {
    return this.logPath;
  }
}