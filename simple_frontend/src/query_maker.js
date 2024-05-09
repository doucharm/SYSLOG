import { authorizedFetch } from "./utils"
export const UserQueryJSON = (id) => ({
    "query":
        `query ($id:UUID!) {
            userById(id: $id) {
                id
                name
                surname
                email
                lastchange
                membership {
                  valid
                  group {
                    name
                    id
                    mastergroup{
                        name
                        id
                    }
                  }
                }

            }
        }`,
    "variables": { "id": id }
})
export const Query_Call = ({id,JSONquery,params}) =>
    authorizedFetch( {
        body: JSON.stringify(JSONquery(id)),
        headers:params
    })
