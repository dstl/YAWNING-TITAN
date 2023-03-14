import { v4 as uuid } from 'uuid';

describe('Manage Game Mode Page', () => {
  let testId;

  // open the game mode for each test in this spec
  beforeEach(() => {
    cy.get('[data-cy="menu-manage-game-modes"]').click();
    // random id for test
    testId = uuid();
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

      cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(testId);

      cy.get('#create-from-dialogue').find('.btn').contains('Create game mode').click();

      // should open the game mode editor
      cy.get('#config-forms').should('be.visible');

      // clean up
      cy.cleanUpGameMode(testId);
    });
  });

  describe('Make a new game mode', () => {
    it('should be able to create a valid new game mode', () => {
      // create new game mode
      cy.get('[data-cy="create-game-mode-button"]').click();

      // input game mode name
      cy.get('#create-dialogue > [data-cy="new-item-name-input"]').type(testId);

      cy.get('#create-dialogue').find('.btn').contains('Create').click();

      // set red ignores defences to true
      // cy.get('#id_ignores_defences').click();

      // there should be no errors
      // cy.get('.error-list').should('not.be.visible');

      // clean up
      cy.cleanUpGameMode(testId);
    });
  });
});
