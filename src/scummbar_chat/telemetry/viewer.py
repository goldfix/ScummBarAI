"""Module: viewer.py
Description: HTML & CSS rendering components for the Streamlit Waterfall Trace Inspector.
Generates interactive Gantt-style timeline bars and hierarchical span trees.
"""

import html


def render_waterfall_html(tree: dict) -> str:
    """Generate a responsive dark-themed Gantt Waterfall timeline HTML block."""
    spans = tree.get("spans", [])
    if not spans:
        return (
            '<div style="background-color: #181825; color: #a6adc8; padding: 20px; '
            'border-radius: 8px; text-align: center; font-family: monospace;">'
            'Nessuno span trovato per questo trace.</div>'
        )

    total_duration_ms = tree.get("total_duration_ms", 1.0)
    mid_duration_ms = total_duration_ms / 2.0

    # Header Axis
    axis_html = f"""
    <div style="display: flex; justify-content: space-between; font-size: 0.78em; color: #a6adc8;
                padding-bottom: 6px; border-bottom: 1px solid #313244; margin-bottom: 10px; font-family: monospace;">
        <span>0 ms</span>
        <span>⏱️ {mid_duration_ms:.1f} ms</span>
        <span>🏁 {total_duration_ms:.1f} ms</span>
    </div>
    """

    rows_html = []
    for span in spans:
        indent_px = span["depth"] * 18
        tree_prefix = "└─ " if span["depth"] > 0 else "● "
        color = span["color"]
        icon = span["icon"]
        name = html.escape(span["name"])
        dur = span["duration_ms"]
        offset_pct = span["offset_pct"]
        width_pct = span["width_pct"]
        status = span["status_code"]

        status_badge = (
            '<span style="color: #f38ba8; font-size: 0.75em; font-weight: bold; margin-left: 6px;">[ERROR]</span>'
            if status == "ERROR"
            else ""
        )

        row = f"""
        <div style="margin-bottom: 8px; padding: 4px 6px; border-radius: 6px; background-color: rgba(255,255,255,0.02);">
            <!-- Label Row -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; font-family: monospace; font-size: 0.82em;">
                <div style="padding-left: {indent_px}px; color: #cdd6f4; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 75%;">
                    <span style="color: #6c7086;">{tree_prefix}</span>
                    <span>{icon} </span>
                    <strong style="color: {color};">{name}</strong>
                    {status_badge}
                </div>
                <div style="color: #bac2de; font-weight: 500; font-size: 0.9em;">
                    {dur:.1f} ms <span style="color: #6c7086; font-size: 0.85em;">({(dur / total_duration_ms) * 100:.0f}%)</span>
                </div>
            </div>
            <!-- Timeline Bar Track -->
            <div style="background-color: #313244; border-radius: 4px; height: 14px; position: relative; width: 100%; overflow: hidden;">
                <div style="position: absolute; left: {offset_pct}%; width: {width_pct}%; background-color: {color};
                            height: 100%; border-radius: 3px; box-shadow: 0 0 6px {color}66;">
                </div>
            </div>
        </div>
        """
        rows_html.append(row)

    container_html = f"""
    <div style="background-color: #181825; border: 1px solid #313244; border-radius: 8px;
                padding: 16px; font-family: 'JetBrains Mono', monospace; box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);">
        {axis_html}
        {''.join(rows_html)}
    </div>
    """
    return container_html
