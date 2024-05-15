import React, { useContext, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import logoImageUrl from "../../img/logoHW.png";
import "../../styles/index.css";

export const Navbar = () => {
	const { store, actions } = useContext(Context)
	const navigate = useNavigate();
	const token = localStorage.getItem("token")

	const handleLogOut = () => {
		actions.logOut();
		navigate('/')
	};

	useEffect(() => {
		if (store.vehicles.length !== 0) {
			actions.favorites();
		}
	}, [store.vehicles])

	return (
		<nav className="navbar navbar-expand navbar-light">
			<div className="container-fluid d-flex">
				<div className="d-flex">
					<Link to="/">
						<img className="logo" src={logoImageUrl} />
					</Link>
					<div className="ms-3">
						<h2 className="navbar-text ms-3 mt-2 mb-2 display-4 text-center"><strong>Friendly Wheels</strong></h2>
					</div>
				</div>
				{token ?
					<div className="d-flex">
						<div className="d-grid gap-3 col-6">
							<div className="btn-group me-1">
								<button className="btn btn-light dropdown-toggle text-dark align-items-center mx-0 mb-1" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
									Mis <i className="fas fa-car-side"></i>
									<span className="px-1 text-dark fs-6" style={{ borderRadius: "30px" }}>{store.myVehicles.length}</span>
								</button>
								<ul className="dropdown-menu">
									{store.myVehicles.length === 0
										? <li className="text-center">(empty)</li>
										: <p>Tengo algo</p>  /* En esta linea iria el map */
									}
								</ul>
							</div>
							<div className="btn-group me-2 text-dark align-items-center fs-4 mb-1">
								<button className="btn btn-light">Añadir <i className="fas fa-car-side"></i></button>
							</div>

							<div className="btn-group me-2 d-flex justify-content-end mb-1">
								<button className="btn btn-light dropdown-toggle text-dark align-items-center mx-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">	
									Mis <i className="fas fa-heart"></i>
									<span className="px-1 text-dark fs-6" style={{ borderRadius: "30px" }}>{store.favorites.length}</span>
								</button>
								<ul className="dropdown-menu">
									{store.favorites.length === 0
										? <li className="text-center">(empty)</li>
										: (store.favorites.map((item, index) => (
											<li key={index} className="d-flex justify-content-between text-primary m-2">
												{item.matricula}
												<button onClick={() => actions.removeFav(item.id)} className="btn p-0 px-1">
													<i className="fas fa-trash"></i>
												</button>
											</li>
										)))
									}
								</ul>
							</div>
							<div className="btn-group d-flex justify-content-end mb-1">
								<button className="btn btn-light me-2" onClick={handleLogOut}>Log Out <i className="fas fa-sign-out-alt"></i></button>
							</div>
						</div>
					</div>
						: (
							<div className="d-grid gap-2 col-3">
								<Link to="/login" className="text-decoration-none">
									<div className="btn-group d-flex mb-3">
										<button className="btn-lg btn-light">Login <i className="fas fa-sign-in-alt"></i></button>
									</div>
								</Link>
								<Link to="/signup" className="text-decoration-none">
									<div className="btn-group d-flex">
										<button className="btn-lg btn-light">Signup <i className="fas fa-sign-in-alt"></i></button>
									</div>
								</Link>
							</div>
						)
					}
			</div>
		</nav >
	);
};
