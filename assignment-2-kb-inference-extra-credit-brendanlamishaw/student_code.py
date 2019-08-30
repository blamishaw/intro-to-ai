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
        # Implementation goes here
        # Not required for the extra credit assignment

    def kb_explain(self, fact_or_rule):
        """
        Explain where the fact or rule comes from

        Args:
            fact_or_rule (Fact or Rule) - Fact or rule to be explained

        Returns:
            string explaining hierarchical support from other Facts and rules
        """
        ####################################################
        # Student code goes here
        string = ""
        FRasserted = False

        if fact_or_rule in self.facts or fact_or_rule in self.rules:

            if isinstance(fact_or_rule, Fact):
                obj = self._get_fact(fact_or_rule)
                if obj.asserted:
                    FRasserted = True
                string += "{}".format(self.formatFact(fact_or_rule, FRasserted)) + '\n'

            elif isinstance(fact_or_rule, Rule):
                obj = self._get_rule(fact_or_rule)
                if obj.asserted:
                    FRasserted = True
                string += "{}".format(self.formatRule(fact_or_rule, FRasserted)) + '\n'

            string = self.supportedBy(obj, string)

        else:
            if fact_or_rule not in self.facts and fact_or_rule not in self.rules:
                if isinstance(fact_or_rule, Fact):
                    string = "Fact is not in the KB"

                elif isinstance(fact_or_rule, Rule):
                    string = "Rule is not in the KB"

                else:
                    string = False

        return string

    def supportedBy(self, obj, string, index=1):
        # Function to recursively find and print supported facts and rules

        for f in obj.supported_by:
            string += '  {}SUPPORTED BY'.format(self.indent(index - 1) if index > 1 else "")
            string += '\n'

            # Print fact (f[0]), check if asserted, and find supported_by
            asserted = False
            if f[0].asserted:
                asserted = True
            string += "{}{}".format(self.indent(index), self.formatFact(f[0], asserted))
            string += '\n'

            if f[0].supported_by:
                index += 1
                string = self.supportedBy(f[0], string, index)

            # Print rule (f[1]), check if asserted, and find supported_by
            asserted = False
            if f[1].asserted:
                asserted = True
            string += "{}{}".format(self.indent(index), self.formatRule(f[1], asserted))
            string += '\n'

            if f[1].supported_by:
                index += 1
                string = self.supportedBy(f[1], string, index)

            # Reset index
            index = 1
        return string

    def indent(self, index):
        # Function to iteratively indent

        string = ''
        for i in range(index):
            string += '    '

        return string

    def formatFact(self, fact, asserted):
        # Pretty print facts

        string = ""
        if isinstance(fact, Fact):
            string = fact.name + ": " + str(fact.statement)

            if asserted:
                string += " ASSERTED"

        return string

    def formatRule(self, rule, asserted=False):
        # Pretty print rules

        string = ""

        if isinstance(rule, Rule):
            string = rule.name + ": "
            string += "("
            for l in rule.lhs:
                if l != rule.lhs[0]:
                    string += ", "
                string += "(" + str(l.predicate)
                for t in l.terms:
                    string += " " + str(t)
                string += ")"
            string += ")"

            string += " -> {}".format(str(rule.rhs))

            if asserted:
                string += " ASSERTED"

        return string

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
        # Implementation goes here
        # Not required for the extra credit assignment
