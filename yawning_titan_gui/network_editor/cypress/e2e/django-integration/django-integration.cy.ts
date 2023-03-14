describe('Django integration', () => {

  it('should have the header and the network editor', () => {
    cy.openEmptyNetwork();

    // check that the django hosts the network editor
    cy.get('.head').should('be.visible');
    cy.get('app-root').should('be.visible');

    cy.cleanUpNetwork();
  });

  /**
   * TEMPORARILY DISABLED
   */
  // it('should send the correct POST body', () => {
  //   // create an empty network
  //   cy.openEmptyNetwork();

  //   // trigger network load
  //   cy.fixture('test-network')
  //     .then(network => {
  //       cy.document()
  //         .then(doc => {
  //           // now $document is a reference to the AUT Document
  //           doc.dispatchEvent(new CustomEvent('networkUpdate', {
  //             detail: JSON.stringify(network)
  //           }));
  //         })
  //         .then(() => {
  //           // intercept the post request
  //           cy.intercept('POST', '/network_editor').as('saveRequest');

  //           // open the node list
  //           cy.get('#node-list-icon').click();

  //           // node list should be visible
  //           cy.get('#node-list-container').should('be.visible');

  //           // get the node with name 'test1'
  //           cy.get('.node-list-item-label').contains('test1').click();

  //           // node properties tab should be open
  //           cy.get('.node-properties-form').should('be.visible');

  //           // get uuid input
  //           cy.get('[data-cy="node-properties-y-position-input"]')
  //             .should('be.visible')
  //             .clear()
  //             .type('600');

  //           // check that the network editor saves the correct network
  //           cy.wait('@saveRequest', { timeout: 10000 }).then(({ request }) => {
  //             // check body
  //             const bodyJson = JSON.parse(request.body);

  //             // check that the correct number of nodes and edges are loaded
  //             expect(bodyJson.nodes).not.to.be.empty;
  //             expect(bodyJson.edges).not.to.be.empty;
  //             expect(Object.keys(bodyJson.nodes).length).to.eq(3);

  //             expect(Object.keys(bodyJson.edges.test1).length).to.eq(2);
  //             expect(Object.keys(bodyJson.edges.test2).length).to.eq(1);
  //             expect(Object.keys(bodyJson.edges.test3).length).to.eq(1);

  //             // check that the input updated the correct property
  //             expect(bodyJson.nodes["test1"].y_pos).to.eq(600);
  //           }).then(() => {
  //             // delete network
  //             cy.cleanUpNetwork();
  //           });
  //         })
  //     });
  // });

  describe('Node Colour Key', () => {
    it('should show the contents of the node key', () => {
      cy.openEmptyNetwork();

      // check if the colour key functions as intended
      cy.get('[data-cy="node-colour-key-expansion-panel"]').click();
      cy.get('[data-cy="node-colour-key-content"]')
        .should('be.visible');

      cy.cleanUpNetwork();
    });
  });
})
