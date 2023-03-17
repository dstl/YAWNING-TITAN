import { v4 as uuid } from 'uuid';

describe('Manage Networks Page', () => {
  it('should open when the manage networks button is pressed', () => {
    cy.get('[data-cy="menu-manage-networks"]').click();
  });

  describe('Make a copy of a network', () => {
    it('should create a copy of the default 18 node network', () => {
      const testName = uuid();
      // open networks
      cy.get('[data-cy="menu-manage-networks"]').click();

      // click on create from
      cy.get('[data-item-name="Default 18-node network"]').find('.create-from').click();

      cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(testName);

      cy.get('#create-from-dialogue').find('.btn').contains('Create network').click();

      cy.wait(500)
        .get('[data-cy="cytoscape-canvas"]').should('be.visible');

      // open the node list
      cy.get('[data-cy="node-list-nav-button"]').click();

      // check that the correct number of nodes are in the copy
      cy.get('.node-list-container').find('.node-list-item-label')
        .then(el => expect(el.length).to.eq(18));

      // check detail of 1 node
      cy.get('.node-list-container').find('.node-list-item-label')
        .contains('0')
        .click()
        .then(() => {
          cy.get('[data-cy="node-properties-uuid-input"]')
            .should('be.visible')
            .then((el: any) => expect(el[0].value).to.eq('00c9f604-83c4-4da9-a71d-9d8376d95253'));
        })
        .then(() => cy.cleanUpNetwork(testName))
    });
  });

  describe('Make a new network', () => {
    it('should create a network from scratch', () => {
      const node1Name = uuid();
      const node2Name = uuid();
      const node3Name = uuid();

      // create a new empty network
      cy.openEmptyNetwork();

      // create nodes on canvas
      cy.get('[data-cy="cytoscape-canvas"]')
        .dblclick(100, 200);
      cy.get('[data-cy="cytoscape-canvas"]')
        .dblclick(100, 350);
      cy.get('[data-cy="cytoscape-canvas"]')
        .dblclick(300, 350);

      // create edges between nodes
      cy.get('[data-cy="cytoscape-canvas"]')
        .click(100, 200);
      cy.get('[data-cy="cytoscape-canvas"]')
        .click(100, 350);
      cy.get('[data-cy="cytoscape-canvas"]')
        .click(300, 350);

      // click away from a node
      cy.wait(500).get('[data-cy="cytoscape-canvas"]')
        .click(200, 200);

      // edit node names
      cy.get('[data-cy="cytoscape-canvas"]')
        .click(100, 200)
        .then(() => {
          cy.get('[data-cy="node-properties-name-input"]')
            .should('be.visible')
            .clear()
            .type(node1Name)
        })

      cy.get('[data-cy="cytoscape-canvas"]')
        .click(100, 350)
        .then(() => {
          cy.get('[data-cy="node-properties-name-input"]')
            .should('be.visible')
            .clear()
            .type(node2Name)
        })

      cy.wait(1000)
        .get('[data-cy="cytoscape-canvas"]')
        .click(300, 350)
        .then(() => {
          cy.get('[data-cy="node-properties-name-input"]')
            .should('be.visible')
            .clear()
            .type(node3Name);

          // intercept the post request
          cy.intercept('POST', '/network_editor').as('saveRequest');
        })
        .then(() => {
          // check that the changes were saved and that they are correct
          cy.wait('@saveRequest', { timeout: 10000 }).then(({ request }) => {
            // check body
            const bodyJson = JSON.parse(request.body);

            console.log(bodyJson)

            // make sure that there are 3 nodes
            expect(Object.keys(bodyJson.nodes).length).to.eq(3);

            // make sure there are 3 nodes with edges
            expect(Object.keys(bodyJson.edges).length).to.eq(3);

            // get the nodes
            const nodeList = [];
            Object.keys(bodyJson.nodes).forEach(key => {
              nodeList.push(bodyJson.nodes[`${key}`]);
            })

            // make sure that the nodes have the names we gave them
            expect(!!nodeList.find((node) => node.name == node1Name)).to.be.true;
            expect(!!nodeList.find((node) => node.name == node2Name)).to.be.true;
            expect(!!nodeList.find((node) => node.name == node3Name)).to.be.true;
          })
            .then(() => {
              // delete network
              cy.cleanUpNetwork();
            });
        })
    });
  });

});
