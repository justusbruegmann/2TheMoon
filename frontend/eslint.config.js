import js from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import eslintConfigPrettier from "eslint-config-prettier/flat";

export default [
  { ignores: ["dist/**", "node_modules/**", "coverage/**"] },

  // Presets (order matters: Vue after TypeScript)
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs["flat/recommended"],

  // TypeScript inside .vue files
  {
    files: ["**/*.vue"],
    languageOptions: { parserOptions: { parser: tseslint.parser } },
  },

  // Team rules: agreed once, enforced for everyone
  {
    rules: {
      eqeqeq: "error",
      "consistent-return": "error",
      // LIVE (step 2): type the camelcase rule here
    },
  },

  // STRUCTURE (step 6): uncomment live with Ctrl+/
  // {
  //   files: ["demo/ui/**/*.{ts,vue}"],
  //   rules: {
  //     "no-restricted-imports": [
  //       "error",
  //       {
  //         patterns: [
  //           {
  //             group: ["**/data/**"],
  //             message: "UI must not import from the data layer, use a service.",
  //           },
  //         ],
  //       },
  //     ],
  //   },
  // },

  // Must be last: switches off rules that clash with Prettier
  eslintConfigPrettier,
];
