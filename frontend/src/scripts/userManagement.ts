


export function isUserLoggedIn() : boolean {
    return localStorage.getItem("user") === "true";
}