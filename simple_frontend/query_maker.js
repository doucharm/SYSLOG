import { authorizedFetch } from "./utils"
import {app_dest} from './variables'
export const GroupQueryJSON = (id) => ({
    "query":
        `query ($id: ID!) {
            groupById(id: $id) {
                id
                name
                lastchange
                valid
                mastergroup {
                    id
                }
                grouptype { 
                    id
                    nameEn
                }
                subgroups {
                    id
                    name
                    lastchange
                    valid
                    mastergroup{
                        id
                    }
                    grouptype
                    {
                        nameEn
                    }
                }
                memberships {
                    id
                    lastchange
                    valid
                    group
                    {
                        id
                        roles{
                            lastchange
                            id
                            roletype{
                                nameEn
                            }
                            group{
                                id
                            }
                        }
                    }
                    user {
                        id
                        name
                        surname
                        email
                        lastchange
                        roles {
                            lastchange
                            id
                            startdate
                            enddate
                            group
                            {
                                id
                                memberships{
                                    id
                                }
                            }
                            valid
                            roletype {
                              id
                              name
                              nameEn
                            }
                          }
                    }
                }
                
            }
        }`,
    "variables": { "id": id }
})
export const UserQueryJSON = (id) => ({
    "query":
        `query ($id: ID!) {
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
                    roles {
                        lastchange
                        id
                        roletype{
                            nameEn 
                        }
                    }
                    mastergroup{
                        name
                        id
                        roles{
                            lastchange
                            id
                            roletype{
                                nameEn
                            }
                        }
                    }
                  }
                }
                roles {
                    lastchange
                    id
                    valid
                    group{
                        id
                    }
                roletype {
                    nameEn
                }
                }
            }
        }`,
    "variables": { "id": id }
})
export const Query_Call = ({id,JSONquery}) =>
    authorizedFetch(app_dest, {
        body: JSON.stringify(JSONquery(id)),
    })
