import { v4 as uuid } from 'uuid';

describe('End To End', () => {
  it('should be able to set up and run a full end to end run of Yawning Titan', () => {
    // game mode id
    const gameModeName = uuid();
    const networkName = uuid();

    /**
     * Create game mode copy from default
     */
    cy.get('[data-cy="menu-manage-game-modes"]').click();

    // click create from in default game mode list item
    cy.get('[data-item-name="Default Game Mode"]').find('.create-from').click();

    cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(gameModeName);

    cy.get('#create-from-dialogue').find('.btn').contains('Create game mode').click();

    // should open the game mode editor
    cy.get('#config-forms').should('be.visible');

    // return to home page
    cy.get('[data-cy="toolbar-home"]').click();

    /**
     * Create network copy from default
     */

    // open networks
    cy.get('[data-cy="menu-manage-networks"]').click();

    // click on create from
    cy.get('[data-item-name="Default 18-node network"]').find('.create-from').click();

    cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(networkName);

    cy.get('#create-from-dialogue').find('.btn').contains('Create network').click();

    cy.wait(500)
      .get('[data-cy="cytoscape-canvas"]').should('be.visible');

    // return to home page
    cy.get('[data-cy="toolbar-home"]').click();

    /**
     * Yawning Titan Run
     */
    // open page
    cy.get('[data-cy="menu-run-yt"]').click();

    // select the game mode
    cy.get('#game-modes')
      .find(`[data-item-name="${gameModeName}"]`)
      .scrollIntoView()
      .click();

    // select the network
    cy.get('#networks')
      .find(`[data-item-name="${networkName}"]`)
      .scrollIntoView()
      .click();

    // save the agent
    cy.get('[data-cy="save"]')
      .scrollIntoView()
      .click();

    // set time steps to 1000
    cy.get('[data-cy="total_timesteps"]')
      .scrollIntoView()
      .type('1000');

    // set training run loops to 10
    cy.get('[data-cy="training_runs"]')
      .scrollIntoView()
      .type('10');

    // evaluate every 100 episodes
    cy.get('[data-cy="n_eval_episodes"]')
      .scrollIntoView()
      .type('100');

    // press run
    cy.get('[data-cy="run-yt-button"]').click();

    // wait until the run is complete
    cy.get('[data-cy="training-logs-output"]')
      // wait up to 5 minutes for the run to complete
      .contains('Saved trained agent', { timeout: 300000 });

    /**
     * CLEAN UP
     */
    cy.cleanUpGameMode(gameModeName);
    cy.cleanUpNetwork(networkName);
  });
})
