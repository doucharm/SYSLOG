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
    console.log(app_dest)
    const overridenPath = app_dest
    return (
        fetch(overridenPath, newParams) 
    )
}