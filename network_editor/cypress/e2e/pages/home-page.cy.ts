describe('Home Page', () => {
  it('should have the buttons that link to other pages', () => {
    cy.get('[data-cy="menu-documentation"]').should('be.visible');
    cy.get('[data-cy="menu-manage-game-modes"]').should('be.visible');
    cy.get('[data-cy="menu-manage-networks"]').should('be.visible');
  });

  describe('Navigation', () => {
    describe('Navigation Sidebar', () => {
      it('should open the side nav when the sidenav button is clicked', () => {
        cy.get('#sandwich-icon').click().then(() => {
          cy.get('[data-cy="toolbar-home"]').find('.icon-text').should('be.visible');
          cy.get('[data-cy="toolbar-documentation"]').find('.icon-text').should('be.visible');
          cy.get('[data-cy="toolbar-manage-game-modes"]').find('.icon-text').should('be.visible');
          cy.get('[data-cy="toolbar-manage-networks"]').find('.icon-text').should('be.visible');
        });
      });
    });

    describe('Home Button', () => {
      it('should open the homepage', () => {
        // open the networks page
        cy.openEmptyNetwork();

        // click the home button
        cy.get('[data-cy="toolbar-home"]').click();

        // homepage buttons should be visible
        cy.get('[data-cy="menu-documentation"]').should('be.visible');
        cy.get('[data-cy="menu-manage-game-modes"]').should('be.visible');
        cy.get('[data-cy="menu-manage-networks"]').should('be.visible');

        // clean up
        cy.cleanUpNetwork();
      });
    });
  });
});
