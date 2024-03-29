from django.utils.translation import gettext_lazy as _

SOURCE_UNCOMPRESS_CHOICE_ALWAYS = 'y'
SOURCE_UNCOMPRESS_CHOICE_NEVER = 'n'
SOURCE_UNCOMPRESS_CHOICE_ASK = 'a'

SOURCE_UNCOMPRESS_NON_INTERACTIVE_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_ALWAYS, _(message='Always')),
    (SOURCE_UNCOMPRESS_CHOICE_NEVER, _(message='Never'))
)

SOURCE_UNCOMPRESS_INTERACTIVE_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_ALWAYS, _(message='Always')),
    (SOURCE_UNCOMPRESS_CHOICE_NEVER, _(message='Never')),
    (SOURCE_UNCOMPRESS_CHOICE_ASK, _(message='Ask user'))
)
