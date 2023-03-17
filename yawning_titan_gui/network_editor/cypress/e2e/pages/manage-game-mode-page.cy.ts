import { v4 as uuid } from 'uuid';

describe('Manage Game Mode Page', () => {
  let testName;

  // open the game mode for each test in this spec
  beforeEach(() => {
    cy.get('[data-cy="menu-manage-game-modes"]').click();
    // random id for test
    testName = uuid();
  });

  it('should open when the manage game mode button is pressed', () => {
    // should show the New game mode button
    cy.get('[data-cy="create-game-mode-button"]').should('be.visible');
  });

  describe('Filter', () => {
    it('should filter game modes by name', () => {
      // check that only DCBO game mode is shown
      cy.get('[data-cy="manager-page-filter-input"]').type('dcbo');

      // should only show DCBO
      cy.get('[data-item-name="DCBO Agent Config"]').should('be.visible');

      // default should not be visible
      cy.get('[data-item-name="Default Game Mode"]').should('not.be.visible');
    });
  });

  describe('Make game mode from existing', () => {
    it('Copying from the Default Game Mode should have the same values as default game mode', () => {
      // click create from in default game mode list item
      cy.get('[data-item-name="Default Game Mode"]').find('.create-from').click();

      cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(testName);

      cy.get('#create-from-dialogue').find('.btn').contains('Create game mode').click();

      // should open the game mode editor
      cy.get('#config-forms').should('be.visible');

      // clean up
      cy.cleanUpGameMode(testName);
    });
  });

  describe('Make a new game mode', () => {
    /**
     * Function used to check that the section is valid and then going to the next
     */
    function nextSection(skipErrorList = false) {
      // there should be no errors
      if (!skipErrorList) {
        cy.existsButNotVisible('.error-list');
      }

      // press the next button
      cy.get('[data-cy="next-game-mode-button"]').click();
    }

    it('should be able to create a valid new game mode', () => {
      // create new game mode
      cy.get('[data-cy="create-game-mode-button"]').click();

      // input game mode name
      cy.get('#create-dialogue > [data-cy="new-item-name-input"]').type(testName);

      cy.get('#create-dialogue').find('.btn').contains('Create').click();

      /**
       * RED AGENT
       */

      // set red ignores defences to true
      cy.get('[data-cy="agent_attack_ignores_defences"]').click();

      // set spread to true
      cy.get('[data-cy="spread_use"]').click();

      // set do nothing to true
      cy.get('[data-cy="zero_day_use"]').click();

      // set red to target nodes randomly
      cy.get('[data-cy="target_mechanism_random"]').click();

      // go to the next section
      nextSection();

      /**
       * BLUE AGENT
       */

      // set blue scan
      cy.get('[data-cy="action_set_scan"]').click();

      // set blue do nothing
      cy.get('[data-cy="action_set_do_nothing"]').click();

      // reduce standard node discovery chance
      cy.get('[data-cy="immediate_standard_node_input"]')
        .clear()
        .type('0.25')
        .type('{enter}');

      // reduce standard node discovery on scan chance
      cy.get('[data-cy="on_scan_standard_node_input"]')
        .clear()
        .type('0.25')
        .type('{enter}');

      // increade deceptive node discovery on scan chance
      cy.get('[data-cy="on_scan_deceptive_node_input"]')
        .clear()
        .type('0.75')
        .type('{enter}');

      // go to the next section
      nextSection();

      /**
       * GAME RULES
       */
      // set the maximum steps to 1000
      cy.get('[data-cy="game_rules_max_steps"]')
        .clear()
        .type('1000')

      // set game mode to end when high value node is lost
      cy.get('[data-cy="blue_loss_condition_high_value_node_lost"]')
        .click();

      nextSection();

      /**
       * OBSERVATION SPACE
       */
      // set all observation space to true
      cy.get('[data-cy="observation_space_compromised_status"]').click();
      cy.get('[data-cy="observation_space_vulnerabilities"]').click();
      cy.get('[data-cy="observation_space_node_connections"]').click();
      cy.get('[data-cy="observation_space_average_vulnerability"]').click();
      cy.get('[data-cy="observation_space_graph_connectivity"]').click();
      cy.get('[data-cy="observation_space_attacking_nodes"]').click();
      cy.get('[data-cy="observation_space_attacked_nodes"]').click();
      cy.get('[data-cy="observation_space_special_nodes"]').click();
      cy.get('[data-cy="observation_space_red_agent_skill"]').click();

      nextSection();

      /**
       * REWARDS
       */
      // punishment
      cy.get('[data-cy="rewards_for_loss"]')
        .clear()
        .type('100');

      // reward
      cy.get('[data-cy="rewards_for_reaching_max_steps"]')
        .clear()
        .type('100');

      nextSection(true);

      /**
       * RESET
       */
      // set all items to true
      cy.get('[data-cy="on_reset_randomise_vulnerabilities"]').click();
      cy.get('[data-cy="on_reset_choose_new_high_value_nodes"]').click();
      cy.get('[data-cy="on_reset_choose_new_entry_nodes"]').click();

      nextSection(true);

      /**
       * MISCELLANEOUS
       */

      /**
       * TODO
       * the last page should show the finish button
       * the next button is the temporary solution
       */

      cy.get('[data-cy="next-game-mode-button"]').click();

      // clean up
      cy.cleanUpGameMode(testName);
    });
  });
});
