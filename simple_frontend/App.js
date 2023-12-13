import {useState} from 'react'
import { Query_Call,GroupQueryJSON,UserQueryJSON } from './query_maker'
import { id_list_user,id_list_group } from './variables'
const [userFetchContent,userFetchContentState]  = useState(null)
const [groupFetchContent,groupFetchContentState]  = useState(null)
export const App =() =>
{
    return(
        <>
        <button onClick={event => FetchUser} >Send request to get user</button>
        <br />
        <text>{userFetchContent}</text>
        </>
    )
}
const FetchUser = () =>
{
    const pom = Math.floor(Math.random()*id_list_user.length)
    const fetchID=id_list_user[pom]
    Query_Call({id:fetchID,JSONquery:UserQueryJSON}).then
    (
        res => res.json()
    ).then(
        json =>userFetchContentState(json.data.userById)
    )
}
const FetchGroup = () =>
{

}