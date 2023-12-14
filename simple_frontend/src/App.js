import {useState} from 'react'
import { Query_Call,GroupQueryJSON,UserQueryJSON } from './query_maker'
import { id_list_user,id_list_group } from './variables'

export const App =() =>
{
    const [userFetchContent,userFetchContentState]  = useState(null)
    const [groupFetchContent,groupFetchContentState]  = useState(null)
    const FetchUser = () =>
        {
        const pom = Math.floor(Math.random()*id_list_user.length)
        const fetchID=id_list_user[pom]
        Query_Call({id:fetchID,JSONquery:UserQueryJSON}).then
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
        Query_Call({id:fetchID,JSONquery:GroupQueryJSON}).then
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

