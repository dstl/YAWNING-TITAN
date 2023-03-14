describe('Documentation Page', () => {
  it('should open when the documentation button is pressed', () => {
    cy.get('[data-cy="menu-documentation"]').click();
  });
});
