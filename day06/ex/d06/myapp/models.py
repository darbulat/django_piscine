from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest


class UserTip(AbstractUser):
    """My custom User model"""

    NEEDS_POINTS_TO_DOWNVOTE_TIP = 15
    NEEDS_POINTS_TO_DELETE_TIP = 30
    UPVOTE_POINTS = 5
    DOWNVOTE_POINTS = 2

    rep_points = models.IntegerField(null=False, default=0)

    def increase_rep(self):
        self.rep_points += self.UPVOTE_POINTS
        self.save()

    def decrease_rep(self):
        self.rep_points -= self.DOWNVOTE_POINTS
        self.save()


class TipModel(models.Model):
    content = models.TextField(null=False)
    author = models.ForeignKey(
        UserTip,
        on_delete=models.CASCADE,
        null=False,
        # related_name='tip'
    )
    date = models.DateTimeField(auto_now_add=True)
    up_votes = models.ManyToManyField('UpVoteModel')
    down_votes = models.ManyToManyField('DownVoteModel')
    updated_at = models.DateTimeField(auto_now=True)

    def upvote(self, user):
        try:
            down_vote: DownVoteModel = self.down_votes.get(author=user)
            down_vote.delete()
        except DownVoteModel.DoesNotExist as e:
            pass
        try:
            up_vote: UpVoteModel = self.up_votes.get(author=user)
            up_vote.delete()
        except UpVoteModel.DoesNotExist as e:
            up_vote = UpVoteModel(author=user)
            up_vote.save()
            self.up_votes.add(up_vote)
            self.save()

    def downvote(self, user):
        try:
            up_votes: UpVoteModel = self.up_votes.get(author=user)
            up_votes.delete()
        except UpVoteModel.DoesNotExist as e:
            pass
        try:
            down_vote: DownVoteModel = self.down_votes.get(author=user)
            down_vote.delete()
        except DownVoteModel.DoesNotExist as e:
            down_vote = DownVoteModel(author=user)
            down_vote.save()
            self.down_votes.add(down_vote)
            self.save()


class UpVoteModel(models.Model):
    author = models.ForeignKey(UserTip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class DownVoteModel(models.Model):
    class Meta:
        permissions = [('can_down_vote', 'Can downvote tip')]

    author = models.ForeignKey(UserTip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        tip = TipModel.objects.filter(down_votes__tipmodel__id=self.pk).distinct()
        print(tip)
        print(self.pk)

    def delete(self, using=None, keep_parents=False):
        print("delete")
        super(DownVoteModel, self).delete(using, keep_parents)
