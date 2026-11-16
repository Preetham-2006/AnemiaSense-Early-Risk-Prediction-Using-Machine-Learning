import { Bell } from "lucide-react";

export default function Topbar() {

  const user =
    JSON.parse(
      localStorage.getItem("user") || "{}"
    );

  return (
    <header className="topbar">

      <div>
        <span className="topbar-label">
          Patient Portal
        </span>
      </div>

      <div className="topbar-right">

        <button className="icon-button">
          <Bell size={19} />
        </button>

        <div className="user-mini">

          <div className="avatar">
            {user.name
              ? user.name.charAt(0).toUpperCase()
              : "P"}
          </div>

          <div>
            <strong>
              {user.name || "Patient"}
            </strong>

            <span>
              Patient
            </span>
          </div>

        </div>

      </div>

    </header>
  );
}