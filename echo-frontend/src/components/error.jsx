import { Link } from "react-router-dom";

const Error = () => {
    return (
        <section className="error">
            <h1>Error 404</h1>
            <Link to= '/'>Back home</Link>
        </section>
    )
}

export default Error