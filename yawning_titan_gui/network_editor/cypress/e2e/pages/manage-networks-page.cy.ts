describe('Manage Networks Page', () => {
  it('should open when the manage networks button is pressed', () => {
    cy.get('[data-cy="menu-manage-networks"]').click();
  });
});
