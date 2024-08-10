# Generated by Django 4.2.14 on 2024-08-06 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "report_type",
                    models.CharField(
                        choices=[
                            ("post", "帖子"),
                            ("circle", "圈子"),
                            ("comment", "评论"),
                            ("user", "用户"),
                        ],
                        max_length=50,
                        verbose_name="举报类型",
                    ),
                ),
                (
                    "reason",
                    models.TextField(blank=True, null=True, verbose_name="举报理由"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "待处理"),
                            ("approved", "已批准"),
                            ("rejected", "已拒绝"),
                        ],
                        default="pending",
                        max_length=50,
                        verbose_name="举报状态",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "reported_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reporters",
                        to="app.customuser",
                        verbose_name="被举报对象",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reports",
                        to="app.customuser",
                        verbose_name="举报者",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserLikeUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="点赞时间"),
                ),
                (
                    "liked_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likers",
                        to="app.customuser",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked_users",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "liked_user")},
            },
        ),
        migrations.CreateModel(
            name="UserLikePost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="点赞时间"),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likers",
                        to="app.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked_posts",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "post")},
            },
        ),
        migrations.CreateModel(
            name="UserLikeComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="点赞时间"),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likers",
                        to="app.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked_comments",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "comment")},
            },
        ),
        migrations.CreateModel(
            name="UserLikeCircle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="点赞时间"),
                ),
                (
                    "circle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likers",
                        to="app.circle",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked_circles",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "circle")},
            },
        ),
        migrations.CreateModel(
            name="UserFollowUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="关注时间"),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following_users",
                        to="app.customuser",
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("follower", "following")},
            },
        ),
        migrations.CreateModel(
            name="UserFollowCircle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="关注时间"),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following_circles",
                        to="app.customuser",
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to="app.circle",
                    ),
                ),
            ],
            options={
                "unique_together": {("follower", "following")},
            },
        ),
        migrations.CreateModel(
            name="UserCollectPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="收藏时间"),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collecters",
                        to="app.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collected_posts",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "post")},
            },
        ),
        migrations.CreateModel(
            name="UserCollectComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="收藏时间"),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collecters",
                        to="app.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collected_comments",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "comment")},
            },
        ),
        migrations.CreateModel(
            name="UserCollectCircle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="收藏时间"),
                ),
                (
                    "circle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collecters",
                        to="app.circle",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collected_circles",
                        to="app.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "circle")},
            },
        ),
    ]
