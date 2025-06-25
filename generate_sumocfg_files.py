vehicle_counts = [50, 100, 500, 1000]

for count in vehicle_counts:
    cfg_content = f"""<configuration>
    <input>
        <net-file value="test.net.xml"/>
        <route-files value="simulation_{count}.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="{count}"/>
    </time>
</configuration>"""

    with open(f"simulation_{count}.sumocfg", "w") as f:
        f.write(cfg_content)

    print(f"✅ Created simulation_{count}.sumocfg")
