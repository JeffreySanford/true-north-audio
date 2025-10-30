import { flat } from '@nx/eslint-plugin';

export default flat([
  {
    files: ['*.ts', '*.tsx'],
    plugins: ['@nx'],
    extends: [
      'plugin:@nx/typescript',
      'plugin:@nx/nest',
      'plugin:@nx/angular',
      'plugin:@nx/mongo',
      'plugin:@typescript-eslint/recommended',
      'prettier'
    ],
    rules: {
      // Add custom rules here
    }
  },
  {
    files: ['*.js', '*.jsx'],
    plugins: ['@nx'],
    extends: [
      'plugin:@nx/javascript',
      'prettier'
    ],
    rules: {
      // Add custom rules here
    }
  },
  {
    files: ['*.html'],
    extends: ['plugin:@nx/angular/template'],
    rules: {
      // Add custom rules here
    }
  }
]);