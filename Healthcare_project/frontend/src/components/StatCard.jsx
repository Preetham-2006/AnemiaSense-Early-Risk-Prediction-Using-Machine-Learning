export default function StatCard({
  title,
  value,
  subtitle,
  icon,
  type = "normal"
}) {

  return (
    <div className={`stat-card ${type}`}>

      <div className="stat-top">

        <span>{title}</span>

        <div className="stat-icon">
          {icon}
        </div>

      </div>

      <h2>{value}</h2>

      <p>{subtitle}</p>

    </div>
  );
}