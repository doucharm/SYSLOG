import { app_dest,bearer_token } from "./variables"
const globalFetchParams = {
    URL:app_dest,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+bearer_token

    },
    cache: 'no-cache',
    redirect: 'follow',
}


export const authorizedFetch = (path, params) => {
    const newParams = { ...globalFetchParams, ...params }
    const overridenPath = app_dest 
    return (
        fetch(overridenPath, newParams) 
    )
}