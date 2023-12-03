from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from django.contrib import messages

class CartObserver(ABC):
    @abstractmethod
    def notify(self, request, total_price):
        pass

class BudgetExceededObserver(CartObserver):
    def notify(self, request, total_price):
        user_budget = request.user.userprofile.budget
        if total_price > user_budget:
            messages.warning(request,f'Warning: Your total cart price ({total_price}) has exceeded your budget ({user_budget}).')