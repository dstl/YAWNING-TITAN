describe('Django integration', () => {
  it('should open the page', () => {
    // check if the django server is up
    cy.visit('http://localhost:8000')
  });

  it('should have the header and the network editor', () => {
    // check that the django hosts the node editor
    cy.get('.head').should('be.visible');
    cy.get('app-root').should('be.visible');
  });

  /**
   * TEMPORARILY DISABLED
   */
  // it('should send the correct POST body', () => {
  //   // intercept the post request
  //   cy.intercept('POST', '/node_editor/').as('saveRequest');

  //   // trigger network load
  //   cy.fixture('test-network').then(network => {
  //     cy.document()
  //     .then(doc => {
  //       // now $document is a reference to the AUT Document
  //       doc.dispatchEvent(new CustomEvent('networkUpdate', {
  //         detail: JSON.stringify(network)
  //       }));
  //     });
  //   });

  //   // nodes should be visible on the list
  //   cy.get('.node-list-item').should('be.visible');

  //   // press the save button
  //   cy.get('.save-button').click();

  //   // check that the node editor saves the correct network
  //   cy.wait('@saveRequest').then(({ request }) => {
  //     // check body
  //     const body = request.body;
  //     // check that the correct number of nodes and edges are loaded
  //     expect(body.nodes).not.to.be.empty
  //     expect(body.edges).not.to.be.empty
  //     expect(Object.keys(body.nodes).length).to.eq(3)

  //     expect(Object.keys(body.edges.test1).length).to.eq(2)
  //     expect(Object.keys(body.edges.test2).length).to.eq(1)
  //     expect(Object.keys(body.edges.test3).length).to.eq(1)
  //   });
  // });
})
