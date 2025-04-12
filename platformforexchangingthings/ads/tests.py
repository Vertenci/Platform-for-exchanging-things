import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Ad, ExchangeProposal


# class AdTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client.login(username='testuser', password='testpassword')
#
#         self.ad = Ad.objects.create(
#             user=self.user,
#             title="Тестовое объявление",
#             description="Описание тестового объявления",
#             category="Электроника",
#             condition="Новое",
#             image_url="test_image.jpg",
#             is_draft=False
#         )
#
#     def test_create_ad(self):
#         image_path = os.path.join(settings.MEDIA_ROOT, 'ad/ad_images/apex.png')
#
#         with open(image_path, 'rb') as img:
#             image_file = SimpleUploadedFile(
#                 name='apex.png',
#                 content=img.read(),
#                 content_type='image/png'
#             )
#
#             response = self.client.post(reverse('create_ad'), {
#                 'title': 'Новое объявление',
#                 'description': 'Описание нового объявления',
#                 'category': 'Книги',
#                 'condition': 'Б/У',
#                 'image_url': image_file,
#             })
#
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Ad.objects.count(), 2)
#
#     def test_edit_ad(self):
#         response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
#             'title': 'Обновление объявления',
#             'description': 'Описание обновленного объявления',
#             'category': 'Электроника',
#             'condition': 'Новое',
#             'image_url': 'updated_image.jpg'
#         })
#
#         self.assertEqual(response.status_code, 302)
#         self.ad.refresh_from_db()
#         self.assertEqual(self.ad.title, 'Обновление объявления')
#
#     def test_delete_ad(self):
#         response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())
#
#     def test_search_ads(self):
#         response = self.client.get(reverse('ads_list'), {'keyword': 'Тестовое'})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.ad.title)
#
#         response = self.client.get(reverse('ads_list'), {'category': 'Электроника'})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.ad.title)
#
#         response = self.client.get(reverse('ads_list'), {'condition': 'Новое'})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.ad.title)


class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title="Объявление 1",
            description="Описание 1",
            category="Электроника",
            condition="Новое",
            image_url="image1.jpg",
            is_draft=False
        )

        self.ad2 = Ad.objects.create(
            user=self.user2,
            title="Объявление 2",
            description="Описание 2",
            category="Книги",
            condition="Б/У",
            image_url="image2.jpg",
            is_draft=False
        )

        login_successful = self.client.login(username='user1', password='password1')

    def test_create_exchange_proposal(self):
        response = self.client.post(reverse('create_exchange_proposal', args=[self.ad2.id]), {
            'ad_sender': self.ad1.id,
            'comment': 'Предлагаю обмен',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

        proposal = ExchangeProposal.objects.first()
        self.assertEqual(proposal.ad_sender, self.ad1)
        self.assertEqual(proposal.ad_receiver, self.ad2)
        self.assertEqual(proposal.comment, 'Предлагаю обмен')
        self.assertEqual(proposal.status, 'Ожидает')

    def test_update_exchange_proposal_status(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Предлагаю обмен',
            status='Ожидает'
        )

        self.client.logout()
        self.client.login(username='user2', password='password2')

        response = self.client.get(reverse('update_exchange_proposal', args=[proposal.id, 'Принята']))

        self.assertEqual(response.status_code, 302)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'Принята')
