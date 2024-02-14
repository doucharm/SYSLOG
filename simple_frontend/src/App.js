import {useState} from 'react'
import { Query_Call,GroupQueryJSON,UserQueryJSON, BadQuery } from './query_maker'
import { id_list_user,id_list_group,list_bearer_token } from './variables'
const CreateHeader=()=> {
    const pom = Math.floor(Math.random()*2)
    const bearer_token=list_bearer_token[pom]
    const pom2 = Math.floor(Math.random()*id_list_user.length)
    const user_id=id_list_user[pom2]
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ bearer_token,
        'user_id': user_id
    }
}
export const App =() =>
{
    const [userFetchContent,userFetchContentState]  = useState(null)
    const [groupFetchContent,groupFetchContentState]  = useState(null)
    const FetchUser = () =>
        {
        const pom = Math.floor(Math.random()*id_list_user.length)
        const fetchID=id_list_user[pom]
        Query_Call({id:fetchID,JSONquery:UserQueryJSON,params:CreateHeader()}).then
        (
            res => res.json()
        ).then(
            json =>userFetchContentState(JSON.stringify(json))
        )
        }
    const FetchGroup = () =>
        {
            const pom = Math.floor(Math.random()*id_list_group.length)
        const fetchID=id_list_group[pom]
        Query_Call({id:fetchID,JSONquery:GroupQueryJSON,params:CreateHeader()}).then
        (
            res => res.json()
        ).then(
            json =>groupFetchContentState(JSON.stringify(json))
        )
        }
    return(
        <>
        <button onClick={event => FetchUser()} >Send request to get user</button>
        <br />
        <text>{userFetchContent}</text>
        <br/>
        <button onClick={event => FetchGroup()} >Send request to get group</button>
        <br />
        <text>{groupFetchContent}</text>
        </>
    )

    }
