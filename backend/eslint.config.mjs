
import nxPlugin from '@nx/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import tsEslintPlugin from '@typescript-eslint/eslint-plugin';
import prettierPlugin from 'eslint-plugin-prettier';

export default [
  {
    files: ['*.ts', '*.tsx'],
    plugins: {
      '@nx': nxPlugin,
      '@typescript-eslint': tsEslintPlugin,
      'prettier': prettierPlugin,
    },
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
    rules: {
      '@nx/enforce-module-boundaries': 'error',
      '@typescript-eslint/no-unused-vars': 'warn',
      '@typescript-eslint/no-explicit-any': 'warn',
      'prettier/prettier': 'warn',
      // Add custom rules here
    },
  },
  {
    files: ['*.js', '*.jsx'],
    plugins: {
      '@nx': nxPlugin,
      'prettier': prettierPlugin,
    },
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      '@nx/enforce-module-boundaries': 'error',
      'no-unused-vars': 'warn',
      'prettier/prettier': 'warn',
      // Add custom rules here
    },
  },
  {
    files: ['*.html'],
    rules: {
      // Add custom rules here
    },
  },
];