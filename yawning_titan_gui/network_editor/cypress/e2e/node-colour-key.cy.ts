describe('Node Colour Key', () => {
  it('should show the contents of the node key', () => {
    cy.get('[data-cy="node-colour-key-expansion-panel"]').click();

    cy.get('[data-cy="node-colour-key-content"]')
      .should('be.visible');
  });
});
