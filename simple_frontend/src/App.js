import {useState,useEffect} from 'react'
import { Query_Call,UserQueryJSON } from './query_maker'
import { id_list_user,id_list_group,list_bearer_token } from './variables'

const CreateHeader = ({ jwt_index }) => {
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + list_bearer_token[jwt_index],
        'user_id': "89d1f3cc-ae0f-11ed-9bd8-0242ac110002"
    };
};
const Get_Average_Response_Time = ({ response_time, added_time, setAverageTime }) => {
    response_time.push(added_time); // Append added_time to response_time
    if (response_time.length === 0) {
        setAverageTime(0);
    } else {
        const averageTime = response_time.reduce((total, current) => total + current, 0) / response_time.length;
        setAverageTime(averageTime);
    }
};
export const App = () => {
    const [jwt_index, set_jwt_index] = useState(0);
    const [responseStatus, setResponseStatus] = useState('');
    const [responseTime, setResponseTime] = useState('');
    const [responseLength, setResponseLength] = useState(0);
    const [average_time, setAverageTime] = useState(0);
    const [response_time, setResponseTimeArray] = useState([]);
    const [requested_id,set_requested_id] =useState("")
    const FetchUser = () => {
        const starttime = new Date();
        const pom = Math.floor(Math.random() * id_list_user.length);
        var fetchID
        if (requested_id!=="")
        {fetchID=requested_id}
        else
        {fetchID = id_list_user[pom];}
        Query_Call({
            id: fetchID,
            JSONquery: UserQueryJSON,
            params: CreateHeader({ jwt_index })
        }).then(response => {
            const responseTime = new Date() - starttime;
            setResponseTime(responseTime);
            setResponseTimeArray([...response_time, responseTime]); // Update response_time array
            console.log(response_time)
            Get_Average_Response_Time({ response_time: response_time, added_time: responseTime, setAverageTime: setAverageTime });
            const statusCode = response.status;
            setResponseStatus(statusCode);
            response.json().then(res => setResponseLength(JSON.stringify(res).length));
            set_requested_id("")
        });
    };
    const FetchErorSQLi = () => {
        const starttime = new Date();
        Query_Call({
            id: 'mass',
            JSONquery: UserQueryJSON,
            params: CreateHeader({ jwt_index })
        }).then(response => {
            const responseTime = new Date() - starttime;
            setResponseTime(responseTime);
            setResponseTimeArray([...response_time, responseTime]); // Update response_time array
            console.log(response_time)
            Get_Average_Response_Time({ response_time: response_time, added_time: responseTime, setAverageTime: setAverageTime });
            const statusCode = response.status;
            setResponseStatus(statusCode);
            response.json().then(res => setResponseLength(JSON.stringify(res).length));
            set_requested_id("")
        });
    };
    const FetchErorDoS = () => {
        const starttime = new Date();
        Query_Call({
            id: 'wait',
            JSONquery: UserQueryJSON,
            params: CreateHeader({ jwt_index })
        }).then(response => {
            const responseTime = new Date() - starttime;
            setResponseTime(responseTime);
            setResponseTimeArray([...response_time, responseTime]); // Update response_time array
            console.log(response_time)
            Get_Average_Response_Time({ response_time: response_time, added_time: responseTime, setAverageTime: setAverageTime });
            const statusCode = response.status;
            setResponseStatus(statusCode);
            response.json().then(res => setResponseLength(JSON.stringify(res).length));
            set_requested_id("")
        });
    };
    const Fetch100 = () => {
        const id_list = id_list_group.concat(id_list_user);
        for (let i = 0; i < 100; i++) {
            const pom = Math.floor(Math.random() * id_list.length);
            const fetchID = id_list[pom];
            Query_Call({
                id: fetchID,
                JSONquery: UserQueryJSON,
                params: CreateHeader({ jwt_index })
            }).then(response => {
                const statusCode = response.status;
                setResponseStatus(statusCode);
                response.json().then(res => setResponseLength(JSON.stringify(res).length));
            });
        }
    };
    const handleidChange = (event) => {
        set_requested_id(event.target.value);
    };
    
    const Automatic_Request = () => {
        const [running, setRunning] = useState(false);
        useEffect(() => {
        let intervalId;
        
        if (running) {
            intervalId = setInterval(() => {
            FetchUser();
            }, 200);
        }
        return () => {
            clearInterval(intervalId);
        };
        }, [running]);
        const startProcess = () => { setRunning(true);};
        const stopProcess = () => {setRunning(false);};
        return (
        <div>
            <button onClick={startProcess}>Start Process</button>
            <button onClick={stopProcess}>Stop Process</button>
        </div>
        );
    };
    
    return (
        <>
            <input type="text" value={requested_id} onChange={handleidChange} placeholder="Enter UUID"  style={{ padding: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc',  boxShadow: '0px 0px 5px rgba(0, 0, 0, 0.1)' }}/>
            <br/>
            <button onClick={event => FetchUser()}>Create request</button>
            <br />
            <button onClick={event => Fetch100()}>Generate mass requests</button>
            {Automatic_Request()}
            <button onClick={event => FetchErorSQLi()}>SQLi</button>
            <button onClick={event => FetchErorDoS()}>DoS</button>
            <h3>Request Parameters</h3>
            <table>
                <tbody>
                    <tr>
                        <td>JWT: {list_bearer_token[jwt_index]}</td>
                        <br/>
                        <td><button onClick={event => set_jwt_index((jwt_index + 1) % 4)}>Change JWT</button></td>
                    </tr>
                </tbody>
            </table>
            <h3>Response Parameters</h3>
            <table>
                <tbody>
                    <tr><td>Response status:</td> <td>{responseStatus}</td></tr>
                    <tr><td>Response time:</td> <td>{responseTime} ms</td></tr>
                    <tr><td>Response's length:</td> <td>{responseLength} B</td></tr>
                    <tr><td>Average response time:</td> <td>{average_time}</td></tr>
                </tbody>
            </table>
        </>
    );
};
