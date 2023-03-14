import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    // setting to show the efficiency (lazy) button to run all specs in dev mode
    experimentalRunAllSpecs: true,
    env: {
      TEST_URL: 'http://localhost:8000/',
      DOCS_PATH: 'docs/',
      GAME_MODE_PATH: 'game_modes/',
      NETWORKS_PATH: 'networks/'
    }
  },
});
