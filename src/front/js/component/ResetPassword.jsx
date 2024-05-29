import React, { useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Context } from "../store/appContext";

export const ResetPassword = () => {
    const { store, actions } = useContext(Context);
    const [password, setPassword] = useState("");
    const { token } = useParams();
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const success = await actions.resetPassword(token, password);
        if (success) {
            alert("Password has been reset.");
            navigate("/login");
        } else {
            alert("Failed to reset password.");
        }
    };

    return (
        <div>
            <h1>Reset Password</h1>
            <form onSubmit={handleSubmit}>
                <label>New Password:</label>
                <input 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required 
                />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};
