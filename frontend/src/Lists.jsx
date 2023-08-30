import {useEffect, useState} from "react";
import { useOutletContext } from "react-router-dom";
import ListComponent from "./components/ListComponent";

const Lists = () => {
    const [lists, setLists] = useState([]);
    const [apiFetch] = useOutletContext();

    useEffect(() => {
        const fetchData = async () => {
            const response = await apiFetch('grouplist');
            setLists(response.data);
        }
        fetchData();
        // console.log(lists)
    }, [])

    useEffect(() => {
        // This effect watches for changes in the 'lists' state variable
        // console.log(lists);
      }, [lists]); // Include 'lists' as a dependency
    
    return (
    <main className="Lists">
        <ListComponent lists={lists}/>
    </main>
    )

    
}

export default Lists