/*
This config is evaluated from top to bottom. This means that later entries can override earlier ones.
*/

import { defineConfig, globalIgnores } from "eslint/config";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-config-prettier/flat";


export default defineConfig([
  // Do not check these folders
  globalIgnores(["dist/**", "node_modules/**", "coverage/**", "test-results/**"]),

  // Use the recommended rules for TypeScript. This also registers the TS parser,
  // which is needed for ESLint to read .ts files at all.
  tseslint.configs.recommended,

  // Recommended rules for Vue. Registers the .vue parser, which handles
  // <template> / <script> blocks.
  pluginVue.configs["flat/recommended"],

  // Inside a .vue file, the Vue parser interprets all <script> blocks as plain JavaScript by default.
  // Therefore, typescript would be parsed as plain JavaScript and every type annotation would throw errors.
  {
    files: ["**/*.vue"],
    languageOptions: { parserOptions: { parser: tseslint.parser } },
  },

  // Manually enabled rules go here
  {
    files: ["**/*.{js,ts,vue}"],
    rules: {
      eqeqeq: "error", // require === or !== instead of == or !=
      "no-var": "error", // use let / const, never var
      "prefer-const": "error", // use const when a variable is never reassigned
      "no-debugger": "error", // no debugger statements in committed code
    },
  },

  // Must stay last: switches off the rules that would fight with Prettier over formatting.
  prettier,
]);
