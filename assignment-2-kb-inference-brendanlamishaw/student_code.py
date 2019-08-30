import read, copy
from util import *
from logical_classes import *

verbose = 0


class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Student code goes here

        if isinstance(fact_or_rule, Fact) and fact_or_rule in self.facts:
            fact = self._get_fact(fact_or_rule)
            self.kb_remove(fact)

    def kb_remove(self, fact_or_rule):

        # Retract Fact that's asserted and supported
        if fact_or_rule.supported_by:
            if fact_or_rule.asserted:
                fact_or_rule.asserted = False
            return

        if isinstance(fact_or_rule, Fact) and fact_or_rule in self.facts:
            if fact_or_rule.supports_facts:
                for f in fact_or_rule.supports_facts:
                    for support in f.supported_by:
                        fact_thing = support[0]
                        if fact_thing == fact_or_rule:
                            f.supported_by.remove(support)
                    if len(f.supported_by) == 0 and not f.asserted:
                        self.kb_remove(f)
            if fact_or_rule.supports_rules:
                for r in fact_or_rule.supports_rules:
                    for support in r.supported_by:
                        rule_thing = support[0]
                        if rule_thing == fact_or_rule:
                            r.supported_by.remove(support)
                    if len(r.supported_by) == 0 and not r.asserted:
                        self.kb_remove(r)

            self.facts.remove(fact_or_rule)

        elif isinstance(fact_or_rule, Rule) and fact_or_rule in self.rules:
            if fact_or_rule.supports_facts:
                for f in fact_or_rule.supports_facts:
                    for support in f.supported_by:
                        fact_thing = support[1]
                        if fact_thing == fact_or_rule:
                            f.supported_by.remove(support)
                    if len(f.supported_by) == 0 and not f.asserted:
                        self.kb_remove(f)
            if fact_or_rule.supports_rules:
                for r in fact_or_rule.supports_rules:
                    for support in r.supported_by:
                        rule_thing = support[1]
                        if rule_thing == fact_or_rule:
                            r.supported_by.remove(support)
                    if len(r.supported_by) == 0 and not r.asserted:
                        self.kb_remove(r)

            self.rules.remove(fact_or_rule)

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        newLHS = []
        bindingsLeft = match(rule.lhs[0], fact.statement)

        if len(rule.lhs) == 1 and bindingsLeft:
            state = instantiate(rule.rhs, bindingsLeft)
            newFact = Fact(state, [[fact, rule]])
            kb.kb_add(newFact)
            kb._get_fact(newFact)
            fact.supports_facts.append(newFact)
            rule.supports_facts.append(newFact)

        elif bindingsLeft:
            # bindingsRight = match(rule.rhs, fact.statement)
            for rlhs in rule.lhs[1:]:
                # bindingsLeft = match(rlhs, fact.statement)
                if bindingsLeft:
                    state = instantiate(rlhs, bindingsLeft)
                    newLHS.append(state)
            newRHS = instantiate(rule.rhs, bindingsLeft)
            newRule = Rule([newLHS, newRHS], [[fact, rule]])
            kb.kb_add(newRule)
            kb._get_rule(newRule)
            fact.supports_rules.append(newRule)
            rule.supports_rules.append(newRule)






















