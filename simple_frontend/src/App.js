import {useState} from 'react'
import { Query_Call,GroupQueryJSON,UserQueryJSON } from './query_maker'
import { id_list_user,id_list_group,list_bearer_token } from './variables'

const CreateHeader=({jwt_index})=> {

    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ list_bearer_token[jwt_index],
        'user_id': "89d1f3cc-ae0f-11ed-9bd8-0242ac110002"
    }
}
export const App =() =>
{
    const [jwt_index,set_jwt_index] = useState(0)
    const [responseStatus, setResponseStatus] = useState('');
    const [responseTime, setResponseTime] = useState('');
    const [responseLength, setResponseLength] = useState(0);
    const FetchUser = () =>
        {

        const starttime= new Date()
        const pom = Math.floor(Math.random()*id_list_user.length)
        const fetchID=id_list_user[pom]

        Query_Call({
            id:fetchID,
            JSONquery:UserQueryJSON,
            params:CreateHeader({jwt_index})
                    })
        .then(response => {
            const responseTime = new Date() - starttime;
            setResponseTime(responseTime);
            const statusCode = response.status;
            setResponseStatus(statusCode);
            response.json().then( res => setResponseLength(JSON.stringify(res).length))

        }
        )
    }
    const Fetch100 =() => //one user make 100 consecutive requests
    {
        const id_list = id_list_group.concat(id_list_user)
        for ( let i=0;i<100; i++)
        {
            const pom = Math.floor(Math.random()*id_list.length)
            const fetchID=id_list[pom]
            Query_Call({
                id:fetchID,
                JSONquery:UserQueryJSON,
                params:CreateHeader({jwt_index})})
        }
    }
    return(
        <>
        <button onClick={event => FetchUser()} >Create request </button>
        <br />
        <button onClick={event => Fetch100()}>Generate mass requests</button>
        <h3>Request Parameters</h3>
        <table>
            <tr>JWT: {list_bearer_token[jwt_index]} </tr>
            <tr><button onClick = {event => set_jwt_index((jwt_index+1)%4)}>Change JWT</button></tr>

        </table>
        <h3>Response Parameters</h3>
        <table >
            <tbody>
            <tr>Response status: {responseStatus}  </tr>
            <tr>Response time: {responseTime}  ms </tr>
            <tr>Response's length:  {responseLength} B </tr>
            </tbody>
        </table>
        </>
    )

    }

