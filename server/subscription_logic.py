from shopify_api import shopify_graphql_request
import logging

def get_customer_subscriptions(customer_id):
    all_matches = []
    has_next_page = True
    after_cursor = None

    while has_next_page:
        query = """
        query GetSubscriptions($after: String) {
          subscriptionContracts(first: 50, after: $after) {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              node {
                id
                status
                nextBillingDate
                customer {
                  id
                  email
                }
                lines(first: 5) {
                  edges {
                    node {
                      title
                      quantity
                    }
                  }
                }
              }
            }
          }
        }
        """

        variables = {"after": after_cursor} if after_cursor else {}

        try:
            response = shopify_graphql_request(query, variables)
            logging.debug(f"Shopify response: {response}")

            contracts = response.get("data", {}).get("subscriptionContracts", {})
            if not contracts:
                logging.warning("No subscriptionContracts returned")
                break

            for edge in contracts.get("edges", []):
                try:
                    contract = edge["node"]
                    contract_customer_id = contract["customer"]["id"].split("/")[-1]
                    if contract_customer_id == str(customer_id):
                        all_matches.append(contract)
                except Exception as e:
                    logging.warning(f"Error parsing contract: {e}")

            has_next_page = contracts.get("pageInfo", {}).get("hasNextPage", False)
            after_cursor = contracts.get("pageInfo", {}).get("endCursor")

        except Exception as e:
            logging.exception("Error during Shopify subscription query")
            break

    return all_matches


def update_subscription(data):
    subscription_id = data.get("subscription_id")  # Must be full GID
    action = data.get("action")

    if not subscription_id or not action:
        return {"error": "Missing subscription_id or action"}, 400

    if action == "pause":
        query = """
        mutation subscriptionContractSetPause($id: ID!) {
          subscriptionContractSetPause(
            id: $id,
            pauseCollection: {
              behavior: MANUAL,
              resumeAt: null
            }
          ) {
            userErrors {
              field
              message
            }
          }
        }
        """
    elif action == "resume":
        query = """
        mutation subscriptionContractResume($id: ID!) {
          subscriptionContractResume(id: $id) {
            userErrors {
              field
              message
            }
          }
        }
        """
    elif action == "cancel":
        query = """
        mutation subscriptionContractCancel($id: ID!) {
          subscriptionContractCancel(id: $id) {
            userErrors {
              field
              message
            }
          }
        }
        """
    else:
        return {"error": "Unsupported action"}, 400

    try:
        variables = {"id": subscription_id}
        result = shopify_graphql_request(query, variables)
        return result
    except Exception as e:
        logging.exception("Error updating subscription")
        return {"error": "Internal Server Error", "details": str(e)}, 500
