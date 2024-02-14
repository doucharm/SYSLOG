import { app_dest,bearer_token} from "./variables"

const globalFetchParams = {
    URL:app_dest,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ bearer_token,
    },
    cache: 'no-cache',
    redirect: 'follow',
}

export const authorizedFetch = (params) => {
    const newParams = { ...globalFetchParams, ...params }
    console.log(params)
    console.log(newParams)
    const overridenPath = app_dest
    return (
        fetch(overridenPath, newParams) 
    )
}