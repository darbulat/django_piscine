from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


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
        print("increase_rep")
        print(self.rep_points)

    def undo_increase_rep(self):
        self.rep_points -= self.UPVOTE_POINTS
        self.save()
        print("undo_increase_rep")
        print(self.rep_points)

    def decrease_rep(self):
        self.rep_points -= self.DOWNVOTE_POINTS
        self.save()
        print("decrease_rep")
        print(self.rep_points)

    def undo_decrease_rep(self):
        self.rep_points += self.DOWNVOTE_POINTS
        self.save()
        print("undo_decrease_rep")
        print(self.rep_points)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        perm_downvote = Permission.objects.get(codename='can_down_vote')
        perm_delete_tip = Permission.objects.get(codename='delete_tipmodel')
        if self.rep_points >= self.NEEDS_POINTS_TO_DOWNVOTE_TIP:
            self.user_permissions.add(perm_downvote)
            print("Now can downvote")
        if self.rep_points >= self.NEEDS_POINTS_TO_DELETE_TIP:
            self.user_permissions.add(perm_delete_tip)
            print("Now can delete tips")
        if self.rep_points < self.NEEDS_POINTS_TO_DELETE_TIP:
            self.user_permissions.remove(perm_delete_tip)
        if self.rep_points < self.NEEDS_POINTS_TO_DOWNVOTE_TIP:
            self.user_permissions.remove(perm_downvote)


class TipModel(models.Model):
    content = models.TextField(null=False)
    author = models.ForeignKey(
        UserTip,
        on_delete=models.CASCADE,
        null=False,
    )
    date = models.DateTimeField(auto_now_add=True)
    up_votes = models.ManyToManyField('UpVoteModel')
    down_votes = models.ManyToManyField('DownVoteModel')
    updated_at = models.DateTimeField(auto_now=True)

    def upvote(self, user):
        try:
            down_vote: DownVoteModel = self.down_votes.get(author=user)
            down_vote.delete()
            self.author.undo_decrease_rep()
        except DownVoteModel.DoesNotExist as e:
            pass
        try:
            up_vote: UpVoteModel = self.up_votes.get(author=user)
            up_vote.delete()
            self.author.undo_increase_rep()
        except UpVoteModel.DoesNotExist as e:
            up_vote = UpVoteModel(author=user)
            up_vote.save()
            self.up_votes.add(up_vote)
            self.save()
            self.author.increase_rep()

    def downvote(self, user):
        try:
            up_votes: UpVoteModel = self.up_votes.get(author=user)
            up_votes.delete()
            self.author.undo_increase_rep()
        except UpVoteModel.DoesNotExist as e:
            pass
        try:
            down_vote: DownVoteModel = self.down_votes.get(author=user)
            down_vote.delete()
            self.author.undo_decrease_rep()
        except DownVoteModel.DoesNotExist as e:
            down_vote = DownVoteModel(author=user)
            down_vote.save()
            self.down_votes.add(down_vote)
            self.save()
            self.author.decrease_rep()

    def delete(self, using=None, keep_parents=False):
        up_votes = len(self.up_votes.all())
        down_votes = len(self.down_votes.all())
        for _ in range(up_votes):
            self.author.undo_increase_rep()
        for _ in range(down_votes):
            self.author.undo_decrease_rep()
        print(f'{up_votes=}, {down_votes=}')
        super().delete(using, keep_parents)


class UpVoteModel(models.Model):
    author = models.ForeignKey(UserTip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DownVoteModel(models.Model):
    class Meta:
        permissions = [('can_down_vote', 'Can downvote tip')]

    author = models.ForeignKey(UserTip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
