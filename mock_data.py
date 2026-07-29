from models.ticket import Ticket


def get_dummy_ticket() -> Ticket:
    return Ticket(
        ticket_id="ADAS-1423",
        summary="Lane Keeping Assist drifts to the left",
        description="""
Vehicle continuously drifts towards the left after driving
for approximately 15 minutes.

Issue reproduced in SIL and HIL.

Expected Behaviour:
Vehicle should remain centered within the lane.

Actual Behaviour:
Vehicle slowly deviates towards the left without steering correction.

Environment:
• Vehicle Speed : 80 km/h
• Weather : Clear
• Road Type : Highway
• Software Version : v2.4.1
""",
        comments=[
            "Customer reported issue during highway testing.",
            "Issue successfully reproduced in SIL.",
            "No CAN communication errors observed.",
            "Camera calibration verified successfully.",
            "Possible steering controller issue.",
            "Need algorithm team investigation."
        ],
        attachments=[
            "sample_images/lka_dashboard.png",
            "sample_images/lka_camera_view.png",
            "sample_images/graphic.png"

        ]
    )