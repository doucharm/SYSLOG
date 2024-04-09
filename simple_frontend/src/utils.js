import { app_dest,bearer_token} from "./variables"

const globalFetchParams = {
    URL:app_dest,
    method: 'POST',
    headers: {

    },
    cache: 'no-cache',
    redirect: 'follow',
}

export const authorizedFetch = (params) => {
    const newParams = { ...globalFetchParams, ...params }

    const overridenPath = app_dest
    return (
        fetch("http://localhost:31120/gql", newParams) 
    )
}