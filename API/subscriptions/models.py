from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL  # this is auth.user


ALLOWED_CUSTOM_GROUPS = True

SUBSCRIPTIONS_MODEL = [
    ("enterprise", "Enterprise Perm"),
    ("standard", "Standard Perm"),
    ("free", "Free Perm"),
    ("ai_free", "Free AI Perm"),
    ("ai_adv", "Advance AI Perm"),
]


# Create your models here.
class SubModel(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, blank=True)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            "content_type__app_label": "subscriptions",
            "codename__in": [x[0] for x in SUBSCRIPTIONS_MODEL],
        },
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        permissions = SUBSCRIPTIONS_MODEL


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sub = models.ForeignKey(SubModel, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}-{self.sub.name}"


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    sub_obj = user_sub_instance.sub
    groups = sub_obj.groups.all()
    if not ALLOWED_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = (
            SubModel.objects.filter(active=True)
            .exclude(id=sub_obj.id)
            .values_list("groups__id", flat=True)
        )
        sub_group_sets = set(subs_qs)
        print(f"SUB GROUP SET: {sub_group_sets}")
        groups_id = groups.values_list("id", flat=True)
        print(f"GROUP SET: {groups_id}")
        current_groups = user.groups.all().values_list("id", flat=True)
        print(f"CURRENT GROUP: {current_groups}")
        groups_id_set = set(groups_id)
        print(f"ID GROUP SET: {groups_id_set}")
        current_groups_set = set(current_groups) - sub_group_sets
        print(f"CURRENT GROUP SET: {current_groups_set}")
        final_group_ids = list(groups_id_set | current_groups_set)
        print(final_group_ids)
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)
