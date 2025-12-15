tables = {
    'USER': {
        'x': 400,
        'y': 40,
        'width': 160,
        'attributes': [
            {'name': 'user_id', 'key': 'PK'},
            {'name': 'email', 'key': ''},
            {'name': 'phone_number', 'key': ''},
            {'name': 'username', 'key': ''},
            {'name': 'display_name', 'key': ''},
            {'name': 'nickname', 'key': ''},
            {'name': 'avatar', 'key': ''},
            {'name': 'bio', 'key': ''},
            {'name': 'is_private', 'key': ''},
            {'name': 'is_content_creator', 'key': ''},
            {'name': 'follower_threshold_met', 'key': ''},
            {'name': 'created_at', 'key': ''},
            {'name': 'updated_at', 'key': ''},
        ]
    },
    'VIDEO': {
        'x': 800,
        'y': 40,
        'width': 160,
        'attributes': [
            {'name': 'video_id', 'key': 'PK'},
            {'name': 'user_id', 'key': 'FK'},
            {'name': 'audio_id', 'key': 'FK'},
            {'name': 'title', 'key': ''},
            {'name': 'description', 'key': ''},
            {'name': 'duration', 'key': ''},
            {'name': 'video_url', 'key': ''},
            {'name': 'thumbnail_url', 'key': ''},
            {'name': 'visibility', 'key': ''},
            {'name': 'like_count', 'key': ''},
            {'name': 'comment_count', 'key': ''},
            {'name': 'share_count', 'key': ''},
            {'name': 'view_count', 'key': ''},
            {'name': 'is_approved', 'key': ''},
            {'name': 'moderation_status', 'key': ''},
            {'name': 'created_at', 'key': ''},
            {'name': 'updated_at', 'key': ''},
        ]
    },
    'AUDIO': {
        'x': 1100,
        'y': 40,
        'width': 160,
        'attributes': [
            {'name': 'audio_id', 'key': 'PK'},
            {'name': 'source_video_id', 'key': 'FK'},
            {'name': 'title', 'key': ''},
            {'name': 'artist', 'key': ''},
            {'name': 'duration', 'key': ''},
            {'name': 'audio_url', 'key': ''},
            {'name': 'is_original', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'HASHTAG': {
        'x': 1100,
        'y': 250,
        'width': 160,
        'attributes': [
            {'name': 'hashtag_id', 'key': 'PK'},
            {'name': 'name', 'key': ''},
            {'name': 'usage_count', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'COMMENT': {
        'x': 800,
        'y': 420,
        'width': 160,
        'attributes': [
            {'name': 'comment_id', 'key': 'PK'},
            {'name': 'video_id', 'key': 'FK'},
            {'name': 'user_id', 'key': 'FK'},
            {'name': 'parent_comment_id', 'key': 'FK'},
            {'name': 'content', 'key': ''},
            {'name': 'is_pinned', 'key': ''},
            {'name': 'is_hidden', 'key': ''},
            {'name': 'created_at', 'key': ''},
            {'name': 'updated_at', 'key': ''},
        ]
    },
    'LIVESTREAM': {
        'x': 400,
        'y': 420,
        'width': 160,
        'attributes': [
            {'name': 'livestream_id', 'key': 'PK'},
            {'name': 'user_id', 'key': 'FK'},
            {'name': 'title', 'key': ''},
            {'name': 'description', 'key': ''},
            {'name': 'stream_url', 'key': ''},
            {'name': 'viewer_count', 'key': ''},
            {'name': 'total_gifts_value', 'key': ''},
            {'name': 'status', 'key': ''},
            {'name': 'started_at', 'key': ''},
            {'name': 'ended_at', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'MESSAGE': {
        'x': 80,
        'y': 420,
        'width': 160,
        'attributes': [
            {'name': 'message_id', 'key': 'PK'},
            {'name': 'sender_id', 'key': 'FK'},
            {'name': 'receiver_id', 'key': 'FK'},
            {'name': 'content', 'key': ''},
            {'name': 'message_type', 'key': ''},
            {'name': 'media_url', 'key': ''},
            {'name': 'is_read', 'key': ''},
            {'name': 'is_deleted', 'key': ''},
            {'name': 'created_at', 'key': ''},
            {'name': 'updated_at', 'key': ''},
        ]
    },
    'REPORT': {
        'x': 1100,
        'y': 420,
        'width': 160,
        'attributes': [
            {'name': 'report_id', 'key': 'PK'},
            {'name': 'reporter_id', 'key': 'FK'},
            {'name': 'reported_user_id', 'key': 'FK'},
            {'name': 'video_id', 'key': 'FK'},
            {'name': 'comment_id', 'key': 'FK'},
            {'name': 'reason', 'key': ''},
            {'name': 'description', 'key': ''},
            {'name': 'status', 'key': ''},
            {'name': 'reviewed_by', 'key': 'FK'},
            {'name': 'created_at', 'key': ''},
            {'name': 'resolved_at', 'key': ''},
        ]
    },
    'PAYMENT_ACCOUNT': {
        'x': 80,
        'y': 40,
        'width': 160,
        'attributes': [
            {'name': 'account_id', 'key': 'PK'},
            {'name': 'user_id', 'key': 'FK'},
            {'name': 'account_type', 'key': ''},
            {'name': 'account_number', 'key': ''},
            {'name': 'balance', 'key': ''},
            {'name': 'is_verified', 'key': ''},
            {'name': 'created_at', 'key': ''},
            {'name': 'updated_at', 'key': ''},
        ]
    },
    'GIFT': {
        'x': 80,
        'y': 680,
        'width': 160,
        'attributes': [
            {'name': 'gift_id', 'key': 'PK'},
            {'name': 'name', 'key': ''},
            {'name': 'icon_url', 'key': ''},
            {'name': 'coin_cost', 'key': ''},
            {'name': 'real_value', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'NOTIFICATION': {
        'x': 400,
        'y': 680,
        'width': 160,
        'attributes': [
            {'name': 'notification_id', 'key': 'PK'},
            {'name': 'user_id', 'key': 'FK'},
            {'name': 'type', 'key': ''},
            {'name': 'content', 'key': ''},
            {'name': 'related_id', 'key': ''},
            {'name': 'is_read', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'FOLLOW': {
        'x': 80,
        'y': 250,
        'width': 160,
        'attributes': [
            {'name': 'follower_id', 'key': 'PK,FK1'},
            {'name': 'following_id', 'key': 'PK,FK2'},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'LIKE': {
        'x': 640,
        'y': 680,
        'width': 160,
        'attributes': [
            {'name': 'user_id', 'key': 'PK,FK1'},
            {'name': 'video_id', 'key': 'PK,FK2'},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'VIDEO_HASHTAG': {
        'x': 1350,
        'y': 250,
        'width': 160,
        'attributes': [
            {'name': 'video_id', 'key': 'PK,FK1'},
            {'name': 'hashtag_id', 'key': 'PK,FK2'},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'BLOCK': {
        'x': 640,
        'y': 40,
        'width': 160,
        'attributes': [
            {'name': 'blocker_id', 'key': 'PK,FK1'},
            {'name': 'blocked_id', 'key': 'PK,FK2'},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'SAVED_VIDEO': {
        'x': 880,
        'y': 680,
        'width': 160,
        'attributes': [
            {'name': 'user_id', 'key': 'PK,FK1'},
            {'name': 'video_id', 'key': 'PK,FK2'},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'GIFT_TRANSACTION': {
        'x': 320,
        'y': 880,
        'width': 160,
        'attributes': [
            {'name': 'transaction_id', 'key': 'PK'},
            {'name': 'sender_id', 'key': 'FK'},
            {'name': 'receiver_id', 'key': 'FK'},
            {'name': 'livestream_id', 'key': 'FK'},
            {'name': 'gift_id', 'key': 'FK'},
            {'name': 'quantity', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'SHARE': {
        'x': 1120,
        'y': 680,
        'width': 160,
        'attributes': [
            {'name': 'user_id', 'key': 'PK,FK1'},
            {'name': 'video_id', 'key': 'PK,FK2'},
            {'name': 'share_type', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'VIEW_HISTORY': {
        'x': 1350,
        'y': 680,
        'width': 160,
        'attributes': [
            {'name': 'user_id', 'key': 'PK,FK1'},
            {'name': 'video_id', 'key': 'PK,FK2'},
            {'name': 'watch_duration', 'key': ''},
            {'name': 'created_at', 'key': ''},
        ]
    },
    'NOT_INTERESTED': {
        'x': 1350,
        'y': 420,
        'width': 160,
        'attributes': [
            {'name': 'user_id', 'key': 'PK,FK1'},
            {'name': 'video_id', 'key': 'FK'},
            {'name': 'hashtag_id', 'key': 'FK'},
            {'name': 'audio_id', 'key': 'FK'},
            {'name': 'created_at', 'key': ''},
        ]
    },
}

relationships = [
    {'source_table': 'VIDEO', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'VIDEO', 'source_attr': 'audio_id', 'target_table': 'AUDIO', 'target_attr': 'audio_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'AUDIO', 'source_attr': 'source_video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'COMMENT', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'COMMENT', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'COMMENT', 'source_attr': 'parent_comment_id', 'target_table': 'COMMENT', 'target_attr': 'comment_id', 'style': 'edgeStyle=loopEdgeStyle;html=1;endArrow=ERmany;startArrow=ERzeroToOne;rounded=1;', 'points': [{'x': 760, 'y': 500}, {'x': 760, 'y': 600}]},
    {'source_table': 'LIVESTREAM', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'PAYMENT_ACCOUNT', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'NOTIFICATION', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'FOLLOW', 'source_attr': 'follower_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'FOLLOW', 'source_attr': 'following_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'LIKE', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'LIKE', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'VIDEO_HASHTAG', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'VIDEO_HASHTAG', 'source_attr': 'hashtag_id', 'target_table': 'HASHTAG', 'target_attr': 'hashtag_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'BLOCK', 'source_attr': 'blocker_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'BLOCK', 'source_attr': 'blocked_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'SAVED_VIDEO', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'SAVED_VIDEO', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'GIFT_TRANSACTION', 'source_attr': 'sender_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'GIFT_TRANSACTION', 'source_attr': 'receiver_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'GIFT_TRANSACTION', 'source_attr': 'livestream_id', 'target_table': 'LIVESTREAM', 'target_attr': 'livestream_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'GIFT_TRANSACTION', 'source_attr': 'gift_id', 'target_table': 'GIFT', 'target_attr': 'gift_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'SHARE', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'SHARE', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'VIEW_HISTORY', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'VIEW_HISTORY', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'NOT_INTERESTED', 'source_attr': 'user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'NOT_INTERESTED', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'NOT_INTERESTED', 'source_attr': 'hashtag_id', 'target_table': 'HASHTAG', 'target_attr': 'hashtag_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'NOT_INTERESTED', 'source_attr': 'audio_id', 'target_table': 'AUDIO', 'target_attr': 'audio_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'MESSAGE', 'source_attr': 'sender_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'MESSAGE', 'source_attr': 'receiver_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'REPORT', 'source_attr': 'reporter_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'REPORT', 'source_attr': 'reported_user_id', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'REPORT', 'source_attr': 'video_id', 'target_table': 'VIDEO', 'target_attr': 'video_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'REPORT', 'source_attr': 'comment_id', 'target_table': 'COMMENT', 'target_attr': 'comment_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
    {'source_table': 'REPORT', 'source_attr': 'reviewed_by', 'target_table': 'USER', 'target_attr': 'user_id', 'style': 'edgeStyle=orthogonalEdgeStyle;html=1;endArrow=ERzeroToMany;endFill=0;startArrow=ERmandOne;startFill=0;rounded=0;', 'points': []},
]

attr_ids = {}

id_counter = 2

cells = []

def add_table(name, x, y, width, attributes):

    global id_counter

    table_id = f'table_{id_counter}'

    id_counter += 1

    height = 26 + 10 + sum(30 if attr['key'] != '' else 26 for attr in attributes)

    cells.append(f'<mxCell id="{table_id}" value="{name}" style="swimlane;html=1;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#e0e0e0;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;align=center;rounded=0;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fontFamily=Verdana;fontSize=14" vertex="1" parent="1">')

    cells.append(f'<mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry" />')

    cells.append('</mxCell>')

    y_pos = 26

    for i, attr in enumerate(attributes):

        attr_id = f'attr_{id_counter}'

        id_counter += 1

        attr_ids[name + '.' + attr['name']] = attr_id

        height_attr = 30 if attr['key'] != '' else 26

        font_style = 'fontStyle=5;' if attr['key'] != '' else ''

        spacing_left = 60 if ',' in attr['key'] else 34

        bottom = 'bottom=1' if i == 0 else 'bottom=0'

        style = f"shape=partialRectangle;top=0;left=0;right=0;{bottom};html=1;align=left;verticalAlign=middle;fillColor=none;spacingLeft={spacing_left};spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;dropTarget=0;{font_style}"

        cells.append(f'<mxCell id="{attr_id}" value="{attr["name"]}" style="{style}" vertex="1" parent="{table_id}">')

        cells.append(f'<mxGeometry y="{y_pos}" width="{width}" height="{height_attr}" as="geometry" />')

        cells.append('</mxCell>')

        label_id = f'label_{id_counter}'

        id_counter += 1

        label_font_style = 'fontStyle=1;' if attr['key'] != '' else ''

        label_style = f"shape=partialRectangle;top=0;left=0;bottom=0;html=1;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[];portConstraint=eastwest;part=1;{label_font_style}"

        cells.append(f'<mxCell id="{label_id}" value="{attr["key"]}" style="{label_style}" vertex="1" connectable="0" parent="{attr_id}">')

        cells.append(f'<mxGeometry width="56" height="{height_attr}" as="geometry" />')

        cells.append('</mxCell>')

        y_pos += height_attr

    # last empty row

    empty_id = f'empty_{id_counter}'

    id_counter += 1

    style = f"shape=partialRectangle;top=0;left=0;right=0;bottom=0;html=1;align=left;verticalAlign=top;fillColor=none;spacingLeft=34;spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;dropTarget=0;"

    cells.append(f'<mxCell id="{empty_id}" value="" style="{style}" vertex="1" parent="{table_id}">')

    cells.append(f'<mxGeometry y="{y_pos}" width="{width}" height="10" as="geometry" />')

    cells.append('</mxCell>')

    label_id = f'label_{id_counter}'

    id_counter += 1

    label_style = "shape=partialRectangle;top=0;left=0;bottom=0;html=1;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[];portConstraint=eastwest;part=1;"

    cells.append(f'<mxCell id="{label_id}" value="" style="{label_style}" vertex="1" connectable="0" parent="{empty_id}">')

    cells.append(f'<mxGeometry width="30" height="10" as="geometry" />')

    cells.append('</mxCell>')

    return table_id

table_ids = {}

for name, info in tables.items():

    table_id = add_table(name, info['x'], info['y'], info['width'], info['attributes'])

    table_ids[name] = table_id

# Now, for relationships, add edges

for rel in relationships:

    source_attr_id = attr_ids[rel['source_table'] + '.' + rel['source_attr']]

    target_attr_id = attr_ids[rel['target_table'] + '.' + rel['target_attr']]

    edge_id = f'edge_{id_counter}'

    id_counter += 1

    cells.append(f'<mxCell id="{edge_id}" value="" style="{rel["style"]}" edge="1" parent="1" source="{source_attr_id}" target="{target_attr_id}" if not rel["target_table"] == rel["source_table"] else "{target_attr_id}">')

    cells.append('<mxGeometry relative="1" as="geometry">')

    if 'points' in rel and rel['points']:

        cells.append('<Array as="points">')

        for p in rel['points']:

            cells.append(f'<mxPoint x="{p["x"]}" y="{p["y"]}" />')

        cells.append('</Array>')

    cells.append('</mxGeometry>')

    cells.append('</mxCell>')

print('<mxGraphModel dx="4168" dy="2244" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">')

print('<root>')

print('<mxCell id="0" />')

print('<mxCell id="1" parent="0" />')

for cell in cells:

    print(cell)

print('</root>')

print('</mxGraphModel>')