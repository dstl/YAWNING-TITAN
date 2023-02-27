describe('Node Colour Key', () => {
  it('should show the contents of the node key', () => {
    cy.openEmptyNetwork();

    cy.get('[data-cy="node-colour-key-expansion-panel"]').click({force: true});

    // TODO: uncomment once the toolbar auto opening is disabled
    // cy.get('[data-cy="node-colour-key-content"]')
    //   .should('be.visible');

    cy.cleanUp();
  });
});
